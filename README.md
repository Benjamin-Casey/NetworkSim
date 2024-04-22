# Terms

| Key terms           | Explanation                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------ |
| NNI                 | Network-to-Network Interface                                                               |
| UNI                 | User-to-network interface                                                                  |
| Trunk port/trunking | consolidates multiple links into a single logical link, improving bandwidth and redundancy |
|                     |                                                                                            |


Data packets:
- Header + Payload
- Header:
  - Source + Destination address (IP address in networks, LAN networks they are MACs)
  - Routing info
  - Error detection
  - Fragmentation + reassembly
  - Protocols
  - Transmission

- A switch knows which port to send data to because the service tells it what MAC address is on the other end and each packet targets a MAC.
  - So the switch has config(?) that checks the header of each packet, and then forwards it 





1. Device connects to switch
2. Device sends packet
3. Switch learns device MAC address
4. Switch sends on data.
   1. What if a switch doesn't know where to send the data?
      1. Floods all ports.

