from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psutil
import platform
import os

app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/info")
def get_system_info():
    # Get CPU Model
    cpu_model = platform.processor()
    if platform.system() == "Darwin":
        try:
            # sysctl gives a cleaner name on macOS (e.g. Apple M1)
            output = os.popen("sysctl -n machdep.cpu.brand_string").read().strip()
            if output:
                cpu_model = output
        except Exception:
            pass
    elif platform.system() == "Linux":
        try:
            # Try reading /proc/cpuinfo
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        cpu_model = line.split(":")[1].strip()
                        break
        except Exception:
            pass

    # Get CPU Usage (interval=0.1 to get a quick sample without blocking too long)
    cpu_usage = psutil.cpu_percent(interval=0.1)
    cpu_cores = psutil.cpu_count(logical=False) or psutil.cpu_count(logical=True)

    # Get RAM Usage
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    total_memory_gb = round(memory.total / (1024**3), 1)

    return {
        "cpu_model": cpu_model,
        "cpu_usage": cpu_usage,
        "cpu_cores": cpu_cores,
        "ram_usage": ram_usage,
        "total_memory": total_memory_gb,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
