from bluepy import btle
import time
import binascii

print("Connecting...")
dev = btle.Peripheral("7c:87:ce:13:5e:da") # board3

print("Services...")
for svc in dev.services:
	print(str(svc))

bracelet = btle.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
service = dev.getServiceByUUID(bracelet)

chtruuid = btle.UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")
chtr = service.getCharacteristics(chtruuid)[0]


print(str(chtr.read()))

chtr.write(str.encode("dispensing"))

time.sleep(1)
print(str(chtr.read()))

