

def serverdesc_process(file_name):
	server_desc_list = open(file_name,'r').read().split('@type server-descriptor 1.0')
	return server_desc_list

def serverdesc_search(server_desc_list, router_ip):
	for server_desc in server_desc_list:
		for line in server_desc.split('\n'):
			if(line.startswith('router')):
				if(line.split()[2]==router_ip):
					return server_desc
				else:
					break
	print("NOT FOUND")
	return "NOT FOUND"

def serverdesc_family(found_server_desc):
	for line in found_server_desc.split('\n'):
		if(line.startswith('family')):
			return line.split()[1:]
	return []
'''
def serverdesc_exitpolicy(found_server_desc):
	policy=[]
	for line in found_server_desc.split('\n'):
		if(line.startswith('reject') or line.startswith('accept')):
			policy.append(line)
	return policy
'''

server_desc_list =  serverdesc_process('./server_desc')
found_server_desc = serverdesc_search(server_desc_list,'185.56.80.243')
print(serverdesc_server_descfamily(found_server_desc))
print(serverdesc_exitpolicy(found_server_desc))





