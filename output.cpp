#include <iostream>
using namespace std;

int main() {
int i;
i = 1;
L1:
cout << i;
i = i + 1;

if (((i == 10))) goto L2;
goto L1;
L2:


return 0;
}
#include <iostream>
using namespace std;

int main() {
int i;
i = 1;
L1:
cout << i;
i = i + 1;

if (!((i == 10))) goto L2;
goto L1;
L2:


return 0;
}
#include <iostream>
using namespace std;

int main() {
    int a, b;
    a = 40;
    b = 20;
    cout << a;
    return 0;
}