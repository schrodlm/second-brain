Switch is a **networking hardware** that connects devices on a network by using [[packet switching]] to receive and forward data to the destination device.
![[network_switch.png]]

### Why do we need switches?
If we connect two computers using only cables it there are some big limitations:
1. **distance** (signal will degrade with more distance)
2. cable can connect only **two devices**

These problems can be solved with other more simple devices. 
**Distance**
	- use twisted cables - which will provide much more stable distance 
	- active device - amplifier/repeater which can amplify the signal

**Cable can connect only two devices**
	We introduce multiport repreater - **hub**
	- this device does not understand data going through them and it is basically just a signal amplifier

This seems much easier. The problem is **[[collision]]**. In a system of hubs - only one device is allowed to transmit data. If more device attemt to pass data it will result in a collision.

**Collision domain** - network segment where transmitted data can collide with one another

This means we can not use hubs for the internet. We **need to split the collision domains**.

### Main job
So the main job of a switch is to **divide the network into multiple smaller segments**, each of which is a **seperate collision domain**. This means that devices in one collision domain cannot interfere with the traffic in another.

### Data passing
To pass data between computer in a network we need to be able to **identify each end device**.

We will use [[MAC address | MAC addresses]] for that. 
If we want to send data from PC1 to PC3, we will use **[[frame]]** (simple container for data)
![[switch.drawio 1.png]]

