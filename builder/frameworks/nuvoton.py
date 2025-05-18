from os.path import join, isdir
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
framework_dir = platform.get_package_dir("framework-nuc131bsp")

# Добавление путей к заголовочным файлам BSP
env.Append(
    CPPPATH=[
        join(framework_dir, "Library", "CMSIS", "Include"),
        join(framework_dir, "Library", "Device", "Nuvoton", "NUC131", "Include"),
        join(framework_dir, "Library", "StdDriver", "Inc")
    ]
)

# Добавление исходных файлов драйверов
env.BuildSources(
    join("$BUILD_DIR", "FrameworkNuvoton"),
    join(framework_dir, "Library", "StdDriver", "Src")
)