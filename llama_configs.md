5M
--------

```
config = LlamaConfig(
    vocab_size=32000,
    hidden_size=64,
    intermediate_size=256,
    num_hidden_layers=13,
    num_attention_heads=8,
    max_position_embeddings=512,
    rope_theta=10000.0,
    attention_bias=False,
    mlp_bias=True,
    attn_implementation="flash_attention_2",
    torch_dtype="bfloat16"
)
```

25M
-------------

```
config = LlamaConfig(
    vocab_size=32000,
    hidden_size=256,
    intermediate_size=1024,
    num_hidden_layers=8,
    num_attention_heads=8,
    max_position_embeddings=512,
    rope_theta=10000.0,
    attention_bias=False,
    mlp_bias=True,
    attn_implementation="flash_attention_2",
    torch_dtype="bfloat16"
)
```


60M
---------------

```
config = LlamaConfig(
    vocab_size=32000,
    hidden_size=512,
    intermediate_size=2048,
    num_hidden_layers=6,
    num_attention_heads=8,
    max_position_embeddings=512,
    rope_theta=10000.0,
    attention_bias=False,
    mlp_bias=True,
    attn_implementation="flash_attention_2",
    torch_dtype="bfloat16"
)
```


125M
---------------

```
config = LlamaConfig(
    vocab_size=32000,
    hidden_size=768,
    intermediate_size=3072,
    num_hidden_layers=8,
    num_attention_heads=8,
    max_position_embeddings=512,
    rope_theta=10000.0,
    attention_bias=False,
    mlp_bias=True,
    attn_implementation="flash_attention_2",
    torch_dtype="bfloat16"
)
```


