import vispy
print(vispy.sys_info())
print(vispy.sys_info().find("GL version:  "))
str = vispy.sys_info()
if str[418] == "'" and str[419] == "'":
    print('not import opengl')
#print(vispy.sys_info()[418])