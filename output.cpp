#include <iostream>
using namespace std;
int main() {
	int a;
	int b;
	a = 40;
	b = 20;
	if (!(a>b)) goto L0;
		cout << a << endl;
	goto L1;
	L0:
	L1:
return 0;
}
