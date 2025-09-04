Configuración inicial:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ejecutar el proyecto:

```sh
flask --app src/alpespartners/api run -p 8000
```

Ejecutar en modo debug:

```sh
python -m debugpy --listen 5678 -m flask --app src/alpespartners/api run -p 8000 --reload
```

Simular un llamado a la API de tracking:

```sh
curl --request POST \
  --url http://localhost:8000/tracking/interaccion \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/10.1.1' \
  --cookie session=eyJ1b3ciOnsiIGIiOiJnQVNWVEFBQUFBQUFBQUNNR0dGc2NHVnpjR0Z5ZEc1bGNuTXVZMjl1Wm1sbkxuVnZkNVNNRjFWdWFXUmhaRlJ5WVdKaGFtOVRVVXhCYkdOb1pXMTVsSk9VS1lHVWZaU01DRjlpWVhSamFHVnpsRjJVYzJJdSJ9fQ.aLnuMw.mo5G_WfXlEAExI_1MzpHDfPooT8 \
  --data '{
	"tipo": "CLICK",
	"marca_temporal": "2023-10-27T10:00:00Z",
	"identidad_usuario": {
		"id_usuario": "user_789",
		"id_anonimo": "anon_12345",
		"direccion_ip": "192.168.1.1",
		"agente_usuario": "Mozilla/5.0..."
	},
	"parametros_tracking": {
		"fuente": "instagram",
		"medio": "social",
		"campaña": "navidad_2023",
		"contenido": "banner_principal",
		"termino": "zapatos+running",
		"id_afiliado": "aff_123"
	},
	"elemento_objetivo": {
		"url": "https://tienda.com/producto/123",
		"id_elemento": "banner_principal"
	},
	"contexto": {
		"url_pagina": "https://tienda.com",
		"url_referente": "https://instagram.com",
		"informacion_dispositivo": "mobile;ios;chrome"
	}
}'
```
