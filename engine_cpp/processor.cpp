#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <algorithm>
#include <cmath>

namespace py = pybind11;

py::array_t<uint8_t> apply_all(py::array_t<uint8_t> input, int brightness, float contrast, float saturation) {
    auto buf = input.request();
    auto result = py::array_t<uint8_t>(buf.shape);
    auto res_buf = result.request();
    
    uint8_t *ptr = static_cast<uint8_t *>(buf.ptr);
    uint8_t *res_ptr = static_cast<uint8_t *>(res_buf.ptr);

    // Assuming RGB image (3 channels)
    // We process 3 bytes (R, G, B) at a time
    for (size_t i = 0; i < buf.size; i += 3) {
        // 1. Brightness
        float r = ptr[i] + brightness;
        float g = ptr[i+1] + brightness;
        float b = ptr[i+2] + brightness;

        // 2. Contrast (formula: factor * (pixel - 128) + 128)
        float c_factor = (contrast + 100) / 100.0f; // Scale -100 to 100 range
        r = c_factor * (r - 128) + 128;
        g = c_factor * (g - 128) + 128;
        b = c_factor * (b - 128) + 128;

        // 3. Saturation (simple luminance-based desaturation/oversaturation)
        float lum = 0.299f * r + 0.587f * g + 0.114f * b;
        float s_factor = (saturation + 100) / 100.0f;
        r = lum + s_factor * (r - lum);
        g = lum + s_factor * (g - lum);
        b = lum + s_factor * (b - lum);

        // Clamping to [0, 255]
        res_ptr[i]   = (uint8_t)std::max(0.0f, std::min(255.0f, r));
        res_ptr[i+1] = (uint8_t)std::max(0.0f, std::min(255.0f, g));
        res_ptr[i+2] = (uint8_t)std::max(0.0f, std::min(255.0f, b));
    }
    return result;
}

PYBIND11_MODULE(image_engine_cpp, m) {
    m.def("apply_all", &apply_all);
}