# FILENAME: setattrtest.py
# A test setting class data members via the setattr(object, name, value) function

class MyClass:
	setMe: int

	@classmethod
	def setvar(cls, name: str, value: int):
		setattr(cls, name, value)

mc = MyClass
mc.setvar(name="setMe", value=10)
print(mc.setMe)
