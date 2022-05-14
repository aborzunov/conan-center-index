#include <iostream>
#include <thread_pool.hpp>

int main(void)
{
    thread_pool pool(4);

    auto loop = [] (auto b, auto e)
    {
        for (auto i = b; i < e; i++)
        { std::cout << "Doing " << i << "-th task\n"; }
    };

    pool.parallelize_loop(0, 10, loop, 10);
}
