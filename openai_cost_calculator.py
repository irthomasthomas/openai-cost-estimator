
import click
import tiktoken
import json

# Load an encoding for tokenization
# Replace 'gpt-3.5-turbo' with the model you are using
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

# Function to load pricing data from a JSON file
def load_pricing_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        pricing = {}
        for category in data['language_models'].values():
            for model in category.get('models', []):
                pricing[model['name']] = {
                    'input': model.get('input_price', 0),
                    'output': model.get('output_price', 0)
                }
        for category, details in data['other_models'].items():
            for model_name, model_data in details.items():
                if isinstance(model_data, list):
                    for spec in model_data:
                        pricing[spec['resolution']] = {'image': spec['price_per_image']}
                elif isinstance(model_data, dict):
                    for sub_category, sub_specs in model_data.items():
                        if isinstance(sub_specs, list):
                            for spec in sub_specs:
                                pricing[spec['resolution']] = {'image': spec['price_per_image']}
                        else:
                            pricing[sub_category] = sub_specs
        return pricing

# Load pricing data from the JSON file
PRICING = load_pricing_data('/home/thomas/Development/Projects/llm/openai_cost_estimator/openai-api-prices.json')

def calculate_cost(model, content_length, operation='input'):
    """Calculate the cost based on model, content length, and operation type."""
    rate = PRICING.get(model, {}).get(operation)
    if rate is None:
        raise ValueError('Model or operation type not found in pricing data.')
    return rate * content_length / 1000  # Assuming rate is per 1K tokens

def calculate_token_count(content):
    """Calculate the number of tokens in the content using tiktoken."""
    token_count = len(encoding.encode(content))
    return token_count

@click.command()
@click.argument('content', default='', required=False)
@click.option('--model', prompt='Model name', help='The model/service endpoint.')
@click.option('--operation', default='input', help='Operation type (input/output).')
@click.option('--token-count', default=None, help='Token count (overrides content).', type=int)


def main(model, content, operation, token_count):
    """CLI tool to calculate the cost of using OpenAI API."""
    if token_count is None:
        token_count = calculate_token_count(content)
    cost = calculate_cost(model, token_count, operation)
    click.echo(f"Cost: ${cost:.6f} (USD) for {token_count} tokens.")


if __name__ == '__main__':
    main()