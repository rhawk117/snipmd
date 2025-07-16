### Class method
 **Prefix**: clsdef
n/a

#### Template

```python
@classmethod
def ${1:method_name}(cls, ${2:args}):
	...
```

---
### Static method
 **Prefix**: staticdef
n/a

#### Template

```python
@staticmethod
def ${1:method_name}(${2:args}) -> None:
	...
```

---
### Function
 **Prefix**: def
n/a

#### Template

```python
def ${1:function_name}(${2:args}) -> None:
	...
```

---
### Class
 **Prefix**: class
n/a

#### Template

```python
class ${1:ClassName}(${2:BaseClass}):
	def __init__(self, *, ${3:args}) -> None:
		...

	def ${4:method_name}(self, ${5:args}):
		...
```

---
### Dataclass
 **Prefix**: dclass
n/a

#### Template

```python
@dataclass
class ${1:ClassName}:
	${2:field_name}: ${3:type} = ${4:default_value}

```

---
### Instance Method
 **Prefix**: selfdef
n/a

#### Template

```python
def ${1:method_name}(self, ${2:args}) -> None:
	...
```

---
### Main
 **Prefix**: psvm
n/a

#### Template

```python
def main() -> None:
	${1:pass}

if __name__ == '__main__':
	main()
```