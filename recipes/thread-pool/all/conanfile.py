import os
from conans import ConanFile, tools

class threadpoolConan(ConanFile):
    name = "thread-pool"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/bshoshany/thread-pool"
    description = "A C++17 thread pool for high-performance scientific computing."
    topics = ("C++17", "thread", "pool", "threadpool", "cpp17", "multithreading")
    no_copy_source = True
    license = "MIT"

    settings = "os", "arch", "compiler", "build_type"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def package_id(self):
        self.info.header_only()

    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "7",
            "visual studio": "15",
            "clang": "5",
            "apple-clang": "10",
            }

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, 17)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if not minimum_version:
            self.output.warn(f"{self.name} requires C++17. Your compiler is unknown. Assuming it supports C++17.")
        elif tools.Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(f"{self.name} requires a compiler that supports at least C++17")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self._source_subfolder, strip_root=True)

    def package(self):
        self.copy(pattern="LICENSE*", src=self._source_subfolder, dst="licenses")
        self.copy("*.hpp", src=os.path.join(self._source_subfolder, "./"), dst="include")

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
        self.cpp_info.names["cmake_find_package"] = "ThreadPool"
        self.cpp_info.names["cmake_find_package_multi"] = "ThreadPool"
