#include <iostream>
using namespace std;

int main() {
int a, i;
float b, c;
a = 40;
c = 15.5;
b = c + (float)a;
i = 1;
cout<< "teste" << a << endl;
L1:
cout<< i << endl;
i = i + 1;

if (i == 10) goto L2;
goto L1;
L2:

if (!(((float)a < b))) goto L3;
cout<< a << endl;
cout<< (float)a + b << endl;

goto L4;
L3:
cout<< b - (float)a << endl;
cout<< b << endl;

L4:


return 0;
}