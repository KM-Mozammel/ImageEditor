#pragma once
#include <vector>
#include <memory>
#include <cstdint>
#include <algorithm>

// Base class for all image operations
class Command
{
public:
    virtual ~Command() {}
    virtual void execute(uint8_t *buffer, size_t size) = 0;
};

// Pipeline manages the queue of commands
class Pipeline
{
    std::vector<std::unique_ptr<Command>> commands;

public:
    void add_command(std::unique_ptr<Command> cmd);
    void clear();
    void render(uint8_t *buffer, size_t size);
};