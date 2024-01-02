#include <vector>
#include <iostream>
#include <math.h>

void ignoreme(){}

int main()
{
	constexpr int num = 10;
	std::vector<double> vec(num);

	for(int i = 0; i < num; i++)
	{
		vec[i] = std::sin(i / 10.0); 
	}

	ignoreme();

	for(int i = 0; i < num; i++)
	{
		std::cout << vec[i] << " ";
	}

	std::cout << "\n";
}
