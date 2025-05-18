from os.path import join
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment

# Инициализация окружения
env = DefaultEnvironment()

# Настройка инструментов компиляции
env.Replace(
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-gcc",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    UPLOADER=join("$PIOPACKAGES_DIR", "tool-openocd", "bin", "openocd"),
    UPLOADCMD="$UPLOADER -f interface/cmsis-dap.cfg -f target/nuc131.cfg -c \"program $SOURCES verify reset exit\""
)

# Флаги компиляции
env.Append(
    ARFLAGS=["rcs"],
    ASFLAGS=["-mthumb", "-mcpu=cortex-m0", "-O2"],
    CCFLAGS=["-mthumb", "-mcpu=cortex-m0", "-O2", "-Wall"],
    CXXFLAGS=["-fno-rtti", "-fno-exceptions"],
    LINKFLAGS=["-mthumb", "-mcpu=cortex-m0", "-Wl,--gc-sections"],
    CPPDEFINES=["NUC131"],
    LIBS=["m", "c", "gcc"],
    BUILDERS=dict(
        ElfToBin=Builder(
            action=" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]),
            suffix=".bin"
        )
    )
)

# Цели сборки
target_elf = env.BuildProgram()
target_bin = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)
upload = env.Alias(["upload"], target_bin, "$UPLOADCMD")
AlwaysBuild(upload)
Default(target_bin)