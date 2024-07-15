import base64
import argparse
import os

def decode_base64_to_file(base64_file, output_file):
    with open(base64_file, 'r') as file:
        base64_string = file.read().strip()
    try:
        # Decode the base64 string
        decoded_data = base64.b64decode(base64_string)

        # Write the decoded data to the output file
        with open(output_file, 'wb') as file:
            file.write(decoded_data)

        print(f"File successfully written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Decode a base64 string to a file.")
    parser.add_argument("-i", "--input", help="The base64 encoded file to decode.")
    parser.add_argument("-o", "--output", required=True, help="The output file to write the decoded data.")

    args = parser.parse_args()

    # Check if the output file has the correct extension
    if not args.output.endswith('.mp3'):
        print("Output file must have an .mp3 extension")
        return

    decode_base64_to_file(args.input, args.output)

if __name__ == "__main__":
    main()
