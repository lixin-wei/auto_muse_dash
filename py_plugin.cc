#include <pybind11/pybind11.h>
#include "macos_native_tools.cc"
namespace py = pybind11;

PYBIND11_MODULE(macos_native_tools, m) {
  m.doc() = "MacOS Native Tools"; // optional module docstring

  m.attr("key_code_j") = (int)kVK_ANSI_J;
  m.attr("key_code_f") = (int)kVK_ANSI_F;
  m.attr("key_code_return") = (int)kVK_Return;

  m.def("key_click", &KeyClick, "Simulate key click", py::arg("key_code"), py::arg("duration_ms") = 50);
  m.def("get_screen_pixel", &GetScreenPixel, "Get pixel color", py::arg("x"), py::arg("y"));
}