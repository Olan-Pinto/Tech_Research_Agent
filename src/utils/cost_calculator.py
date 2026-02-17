def calculate_cost(model_name,input_tokens,output_tokens):
    if(model_name=='gpt-4o-mini'):
        input_price = 0.15/1e6
        output_price = 0.6/1e6
    else:
        return "Model not recognized for cost calculation"
    total_cost = input_price*input_tokens + output_price*output_tokens
    return total_cost