#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <memory>
#include <algorithm>
#include <omp.h>

namespace py = pybind11;

// Base Command Class
class Command
{
public:
    virtual ~Command() {}
    virtual void execute(uint8_t *buffer, size_t size) = 0;
};

// Brightness Implementation
class BrightnessCommand : public Command
{
    int v;

public:
    BrightnessCommand(int val) : v(val) {}
    void execute(uint8_t *buffer, size_t size) override
    {
        #pragma omp parallel for
        for (long long i = 0; i < (long long)size; ++i)
        {
            int p = buffer[i] + v;
            buffer[i] = (uint8_t)std::max(0, std::min(255, p));
        }
    }
};

// Contrast Implementation
class ContrastCommand : public Command
{
    float factor;

public:
    ContrastCommand(int val) : factor((val + 100) / 100.0f) {}
    void execute(uint8_t *buffer, size_t size) override
    {
        #pragma omp parallel for
        for (long long i = 0; i < (long long)size; ++i)
        {
            float p = factor * (buffer[i] - 128) + 128;
            buffer[i] = (uint8_t)std::max(0.0f, std::min(255.0f, p));
        }
    }
};

// Saturation Implementation
class SaturationCommand : public Command
{
    float factor;

public:
    SaturationCommand(int val) : factor((val + 100) / 100.0f) {}
    void execute(uint8_t *buffer, size_t size) override
    {
        #pragma omp parallel for
        for (long long i = 0; i < (long long)size; i += 3)
        {
            float r = buffer[i], g = buffer[i + 1], b = buffer[i + 2];
            float lum = 0.299f * r + 0.587f * g + 0.114f * b;
            buffer[i] = (uint8_t)std::max(0.0f, std::min(255.0f, lum + factor * (r - lum)));
            buffer[i + 1] = (uint8_t)std::max(0.0f, std::min(255.0f, lum + factor * (g - lum)));
            buffer[i + 2] = (uint8_t)std::max(0.0f, std::min(255.0f, lum + factor * (b - lum)));
        }
    }
};

// Pipeline Controller
class Pipeline
{
    std::vector<std::unique_ptr<Command>> commands;

public:
    void add_brightness(int v) { commands.push_back(std::make_unique<BrightnessCommand>(v)); }
    void add_contrast(int v) { commands.push_back(std::make_unique<ContrastCommand>(v)); }
    void add_saturation(int v) { commands.push_back(std::make_unique<SaturationCommand>(v)); }
    void clear() { commands.clear(); }
    void render(uint8_t *buffer, size_t size)
    {
        for (auto &cmd : commands)
            cmd->execute(buffer, size);
    }
};

// Pybind11 Module Definition
PYBIND11_MODULE(image_engine_cpp, m)
{
    py::class_<Pipeline>(m, "Pipeline")
        .def(py::init<>())
        .def("add_brightness", &Pipeline::add_brightness)
        .def("add_contrast", &Pipeline::add_contrast)
        .def("add_saturation", &Pipeline::add_saturation)
        .def("clear", &Pipeline::clear)
        .def("render", [](Pipeline &self, py::array_t<uint8_t> input)
             {
            auto buf = input.request();
            self.render(static_cast<uint8_t*>(buf.ptr), buf.size); });
}