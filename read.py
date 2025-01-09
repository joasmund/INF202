import tomllib

with open ("config.toml","rb" ) as f:
    data = tomllib.load(f)

print(data)

