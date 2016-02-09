rem C:\Windows\System32\cmd.exe /E:ON /V:ON /T:0E /K "C:\Program Files\Microsoft SDKs\Windows\v7.0\Bin\SetEnv.cmd"
rem cd C:\Program Files\Microsoft SDKs\Windows\v7.0\

rem set DISTUTILS_USE_SDK=1
rem setenv /x64 /release
cd C:\Users\Pedro\Documents\Workspace\All_Or_Nothing
c:\Python27\python setup_Assignment.py build_ext --inplace
ping 192.168.1.1
