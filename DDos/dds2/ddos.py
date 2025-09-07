import os
import csv
import pyshark

directory = 'captures'  # Directory path where the pcapng files are located
output_file = 'output.csv'  # Output CSV file name

# CSV column names
fieldnames = ['File Name', 'Protocol', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Payload', 'Time Taken']

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.pcapng'):
            filepath = os.path.join(directory, filename)
            cap = pyshark.FileCapture(filepath)

            # Extract information from each packet
            for packet in cap:
                protocol = packet.highest_layer
                src_ip = packet.ip.src if 'ip' in packet else packet.ipv6.src if 'ipv6' in packet else ""
                dst_ip = packet.ip.dst if 'ip' in packet else packet.ipv6.dst if 'ipv6' in packet else ""
                src_port = packet.tcp.srcport if 'tcp' in packet else packet.udp.srcport if 'udp' in packet else ""
                dst_port = packet.tcp.dstport if 'tcp' in packet else packet.udp.dstport if 'udp' in packet else ""

                # Extract payload (if available)
                payload = ""
                if hasattr(packet, 'data'):
                    if hasattr(packet.data, 'data'):
                        payload = packet.data.data

                # Extract time taken
                time_taken = packet.frame_info.time_delta_displayed

                # Write data to CSV file
                writer.writerow({'File Name': filename, 'Protocol': protocol, 'Source IP': src_ip,
                                 'Destination IP': dst_ip, 'Source Port': src_port, 'Destination Port': dst_port,
                                 'Payload': payload, 'Time Taken': time_taken})

                # Print the extracted information
                print(f'File: {filename}, Protocol: {protocol}, Source IP: {src_ip}, Destination IP: {dst_ip}, '
                      f'Source Port: {src_port}, Destination Port: {dst_port}, Payload: {payload}, Time Taken: {time_taken}')

print('Data extraction and CSV creation completed.')

