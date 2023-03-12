clang++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup \
$(python3 -m pybind11 --includes) \
-I/System/Volumes/Data/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Headers/ \
-framework ApplicationServices \
py_plugin.cc -o macos_native_tools.so

clang++ macos_native_tools.cc --std=c++11 -g -framework ApplicationServices -o macos_native_tools