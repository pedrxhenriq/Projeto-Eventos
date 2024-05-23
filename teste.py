import requests

def get_address_from_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

cep = "08561-440"

address_info = get_address_from_cep(cep)
print(address_info)
if address_info:
    print("Detalhes do endereço:")
    print("CEP:", address_info["cep"])
    print("Logradouro:", address_info["logradouro"])
    print("Complemento:", address_info["complemento"])
    print("Bairro:", address_info["bairro"])
    print("Cidade:", address_info["localidade"])
    print("Estado:", address_info["uf"])
else:
    print("Falha ao obter detalhes do endereço.")
