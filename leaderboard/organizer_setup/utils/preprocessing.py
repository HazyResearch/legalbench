import weave

@weave.op()
def preprocess_example(example):
    """
    Preprocesses each example before evaluation.
    This function receives the dataset row and returns both the full data dict
    and individual columns as separate keys.
    """
    
    # Convert example to dict
    if hasattr(example, 'keys'):
        example_dict = dict(example)
    else:
        # Dynamically discover all attributes, excluding built-in Python attributes
        example_dict = {}
        for attr in dir(example):
            # Skip built-in attributes that start with underscore
            if not attr.startswith('_'):
                try:
                    value = getattr(example, attr)
                    # Skip methods and other non-data attributes
                    if not callable(value):
                        example_dict[attr] = value
                except:
                    pass
    
    # Return both the full data dict and individual columns
    result = {"data": example_dict}
    
    # Add individual columns as separate keys
    for key, value in example_dict.items():
        result[key] = value
    
    return result