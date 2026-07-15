#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <memory>
#include <algorithm>

namespace py = pybind11;

class Command
{
public:
    virtual ~Command() {}
    virtual void execute(uint8_t *buffer, size_t size) = 0;
};

// --- Commands ---
class BrightnessCommand : public Command
{
    int v;

public:
    BrightnessCommand(int val) : v(val) {}
    void execute(uint8_t *buffer, size_t size) override
    {
        for (size_t i = 0; i < size; ++i)
        {
            int p = buffer[i] + v;
            buffer[i] = (uint8_t)std::max(0, std::min(255, p));
        }
    }
};

class ContrastCommand : public Command
{
    float factor;

public:
    ContrastCommand(int val) : factor((val + 100) / 100.0f) {}
    void execute(uint8_t *buffer, size_t size) override
    {
        for (size_t i = 0; i < size; ++i)
        {
            float p = factor * (buffer[i] - 128) + 128;
            buffer[i] = (uint8_t)std::max(0.0f, std::min(255.0f, p));
        }
    }
};

// --- Pipeline ---
class Pipeline
{
    std::vector<std::unique_ptr<Command>> commands;

public:
    void add_brightness(int v) { commands.push_back(std::make_unique<BrightnessCommand>(v)); }
    void add_contrast(int v) { commands.push_back(std::make_unique<ContrastCommand>(v)); }
    void clear() { commands.clear(); }
    void render(uint8_t *buffer, size_t size)
    {
        for (auto &cmd : commands)
            cmd->execute(buffer, size);
    }
};

PYBIND11_MODULE(image_engine_cpp, m)
{
    py::class_<Pipeline>(m, "Pipeline")
        .def(py::init<>())
        .def("add_brightness", &Pipeline::add_brightness)
        .def("add_contrast", &Pipeline::add_contrast)
        .def("clear", &Pipeline::clear)
        .def("render", [](Pipeline &self, py::array_t<uint8_t> input)
             {
            auto buf = input.request();
            self.render(static_cast<uint8_t*>(buf.ptr), buf.size); });
}