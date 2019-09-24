import os

os.system('pip install --upgrade pip')

package = os.popen('pip list').readlines()

for prog in  package:
    installed_packages = prog.split()[0]
    print(installed_packages)

    # print(f'pip install --upgrade {installed_packages}')
    os.system(f'pip install --upgrade {prog.split()[0]}')