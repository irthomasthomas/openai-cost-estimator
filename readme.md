# OpenAI API Cost Estimator

This project contains Python scripts to estimate the cost of using the OpenAI API based on various models and operations.

## Usage

### Calculate Cost Based on Text Input

```
python calculate_cost.py --model <model_name> --content <text_input> --operation <input/output>
```

- `model`: The name of the model or service endpoint.
- `content`: The input text.
- `operation`: The type of operation (input or output).

This script uses the OpenAI pricing information to calculate the approximate cost of using the OpenAI API based on the number of tokens in the input text.

### Calculate Cost Based on Image Dimensions

```
python calculate_cost.py --image <image_file> --detail-level <low/high>
```

- `image`: The path to the image file.
- `detail-level`: The level of detail of the image (low or high).

This script calculates the token cost based on the dimensions of the image.

## Pricing Data

The script uses pricing data loaded from a JSON file (`openai-api-prices.json`) to estimate the cost. The pricing data includes the prices per token for different models and operations, as well as the prices per image for different resolutions and detail levels.

## TODO

- [ ] Implement support for more models and services offered by the OpenAI API.
- [ ] Add command-line options to specify the path to the pricing data JSON file.
- [ ] Enhance the error handling and user input validation.
- [ ] Improve the formatting and output of the cost estimation results.
- [ ] Add example usages and instructions in the readme file.
