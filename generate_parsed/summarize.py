import json
import requests
import cohere

# API key for OpenAI
api_key = "tLuVU08Ff26aFLGXX5U7cOD5ricXtCqRCiECzTmY"
co = cohere.Client(api_key)

# Read each line of the "parsed.txt" file
with open("parsed.txt", "r") as file:
    chapters = file.readlines()

# Summarize each chapter
summary_chapters = []
count = 0
for chapter in chapters:
    count = 1
    # Split the chapter into fragments if it is too long
    fragments = []
    if len(chapter) > 512:
        # Split the chapter into fragments of length 256
        fragment_size = 512
        for i in range(0, len(chapter), fragment_size):
            fragment = chapter[i : i + fragment_size]
            dot_index = fragment.rfind(".")
            if dot_index != -1 and dot_index + 1 < fragment_size:
                fragments.append(fragment[:dot_index + 1])
            else:
                fragments.append(fragment)

    else:
        fragments = [chapter]

    # Summarize each fragment
    chapter_summary = ""
    for fragment in fragments:
        prompt = f"""
        This program summarizes text given a paragraph.

        "Recall that in C++, an object is a piece of data in memory, and that it is located at some address in memory. The compiler and runtime determine the location of an object when it is created; aside from deciding whether an object is in the global segment, on the stack, or in the heap segment (the segment used for dynamic memory), the programmer generally does not control the exact location where an object is placed 1. Given the same program and the same inputs to that program, different systems will often end up placing the same objects at different memory locations. In fact, in many implementations, running the same program twice on the same system will result in different addresses for the objects. C++ has placement new, which allows a programmer to initialize a new object in a given memory location. However, even with placement new, the original memory must have been allocated by the programmer, and the programmer does not control the exact address produced by that allocation. Though the programmer does not have control over the address at which an object is located, the programmer does have the ability to query the address on an object once it has been created. In C++, the & (usually pronounced “address-of”) operator can be applied to an object to determine its address: Addresses are usually written in hexadecimal (base-16) notation, with a leading 0x followed by digits in the range 0-9 and a-f, with a representing the value 10, b the value 11, and so on. Most modern machines use 64 bits for an address; since each digit in a hexadecimal number represents four bits (\(2^4 = 16\) values), a 64-bit address requires up to 16 hexadecimal digits. The examples above use only 12 digits, implying that the leading four digits are zeros. "
        In summary: "C++ is a programming language where objects are pieces of data in memory located at a specific address. The location of an object is determined by the compiler and runtime, but the programmer cannot control the exact location. The programmer can use placement new to initialize a new object in a specified memory location, but it still does not control the exact address. The & operator can be applied to an object to determine its address, which is usually written in hexadecimal notation. Most machines use 64 bits for an address and it is represented by 16 hexadecimal digits."

        "A string is a sequence of characters, and it represents text data. C++ has two string abstractions, which we refer to as C-style strings and C++ strings. In the original C language, strings are represented as just an array of characters, which have the type char. The following initializes a string representing the characters in the word hello: Figure 25 Array representation of a string. Character literals are enclosed in single quotes. For example 'h' is the character literal corresponding to the lower-case letter h. The representation of the string in memory is shown in Figure 25. A C-style string has a sentinel value at its end, the special null character, denoted by '\0'. This is not the same as a null pointer, which is denoted by nullptr, nor the character '0', which denotes the digit 0. The null character signals the end of the string, and algorithms on C-style strings rely on its presence to determine where the string ends. A character array can also be initialized with a string literal: If the size of the array is specified, it must have sufficient space for the null terminator. In the second case above, the size of the array is inferred as 6 from the string literal that is used to initialize it. A string literal implicitly contains the null terminator at its end, so both str2 and str3 are initialized to end with a null terminator."
        In summary: This describes C++ strings, which are represented as an array of characters. C-style strings have a special null character ('\0') at the end to signal the end of the string. Character arrays can be initialized with a string literal, which automatically includes the null terminator at the end. The size of the character array must be specified or inferred to have sufficient space for the null terminator."
        
        "{fragment}"
        In summary: """

        response = co.generate(  
        model='xlarge',  
        prompt = prompt,  
        max_tokens=50,  
        temperature=0)


        text = response.generations[0].text.strip().replace('"', '')
        text = text.replace("\n", " ")
        text = " ".join(text.split())
        chapter_summary += text

    summary_chapters.append(chapter_summary)

# Write the summarized chapters to the "summary.txt" file
with open("summary_rand.txt", "w") as file:
    for chapter in summary_chapters:
        file.write(chapter + "\n")
        
    import requests