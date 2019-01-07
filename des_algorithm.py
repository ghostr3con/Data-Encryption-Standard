#!/usr/bin/env python
# coding: utf-8

# ## DES Encryption and Decryption
# 
# #### Since the DES is based on the feistel cipher, all that is needed to specify this algorithm include:
# * Round function
# * Key schedule algorithm
# * Additional Processing 
# * Initial and Final Permutatopm

# In[8]:


from bitstring import BitArray


# In[2]:


def get_IP_vector():
    IP = (58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7)
    return IP


# In[4]:


def init_permute(input_block):
    
    """
    Function to perform initial permutation on the input block 
    """
    # get the initial permutation vector
    IP = get_IP_vector()
    
    # make a bitarray with size equal to input_block
    output_block = BitArray(len(input_block))
    
    # perform permutation
    for index in range(len(input_block)):
        output_block[index] = input_block[IP[index] - 1] 
        
    return output_block
    


# In[6]:


def get_FP_vector():
    FP = (40, 8,    48,     16,     56,     24,     64,     32,
        39,     7,     47,     15,     55,     23,     63,     31,
        38,     6,     46,     14,     54,     22,     62,     30,
        37,     5,     45,     13,     53,     21,     61,     29,
        36,     4,     44,     12,     52,     20,     60,     28,
        35,     3,     43,     11,     51,     19,     59,     27,
        34,     2,     42,     10,     50,     18,     58,     26,
        33,     1,     41,      9,     49,  17,    57,     25)
    
    return FP


# In[8]:


def final_permutation(input_block):
    
    """
    Function to perform the final permutation of the DES encryption
    
    """
    # get the final permutation reference vector
    FP = get_FP_vector()
    
    # make an empty bitarray with the size equal to the input_block
    output_block = BitArray(len(input_block))
    
    # perform final permutation
    for index in range(len(input_block)):
        output_block[index] = input_block[FP[index] - 1]
        
    
    return output_block 


# In[10]:


def get_E_vector():
    """
    Function that returns the reference vector for the expansion function
    """
    
    E = (32,  1,   2,   3,   4,   5,
        4,   5,   6,   7,   8,   9,
        8,   9,   10,  11,  12,  13,
        12,  13,  14,  15,  16,  17,
        16,  17,  18,  19,  20,  21,
        20,  21,  22,  23,  24,  25,
        24,  25,  26,  27,  28,  29,
        28,  29,  30,  31,  32,  1)
    
    return E


# In[12]:


def expansion_function(input_block):
    """
    Function that expands a 32-bit input to a 48-bit input 
    """
    # get expansion reference vector
    E = get_E_vector()
    
    # make a BitArray with the size equal to the length of the expasion vector
    output_block = BitArray(len(E))
    
    # perform expansion based on the reference vector
    for index in range(len(E)):
        output_block[index] = input_block[E[index]-1 ]
    
    return output_block


# In[14]:


def get_S_box():
    
    """
    Function that returns the three dimensional list of S-box reference tables  
    
    S-Box implemented using 3-dimensional lists:
    
    1. 1st dimension - python list with 8 elements representing 8 S-Boxes
    2. 2nd dimension - each of these 8 elements have four lists each, one for each row 
    3. 3rd dimension - each row is a python list holding values between 0-15
    
    The list will have a 3-layer index for value access; if "Sbox" is the list representing thr S-boxes then it
    can be accessed as Sbox[box_number][row][column]
    """
    SBOX = [
# Box-1
[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],
# Box-2

[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],

# Box-3

[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

],

# Box-4
[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],

# Box-5
[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],
# Box-6

[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

],
# Box-7
[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],
# Box-8

[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]

]
    return SBOX


# In[16]:


def s_box_calculation(input_block):
    
    """
    Function that implements S-Box transformation on a 48-bit input block and returns an output block that is the result of the transformation
    
    Each S-box replaces a 6-bit input with a 4-bit output
    
    Given a 6-bit input, the 4-bit output is returned by selecting the row using the outer two bits and the column 
    selecting the inner four bits. 
    
    Input : Input block 
    
    
    """
    # get the s_box_reference list
    s_box = get_S_box()
    
    # make an empty BitArray
    output_block = BitArray(4)
    
    # go throught the input_block every 6 bits 
    for i in range(0, len(input_block) , 6):
        
        # calculate the sbox_num based on the index
        sbox_num = int(i / 6)
        
        # get the segment of the input_block correnpoding to 6-bit
        segment = input_block[i : i+6]
        
    
        # get the outer two bits of this segment
        outer_bits = BitArray(2)
        outer_bits[0] = segment[0]
        outer_bits[1] = segment[-1]
        
        # convert the outer bit to int to represent the row index
        row_index = outer_bits.uint
        
        # get the inner four bits
        inner_bits = segment[1:-1]
        
        # convert the inner bits to int to represent the column index
        column_index = inner_bits.uint
        
        # get the corresponding value from the s_box
        value = s_box[sbox_num][row_index][column_index]
        
        # convert the value to a binary representation
        binary_value = BitArray(4)
        binary_value[0:4] = format(value, '#06b') 
        
        # add the binary_value to the output
        output_block[i:i+4] = binary_value

    
    
    return output_block
        
    


# In[18]:


def get_P_box():
    """
    Function that returns the permutation (straight P) reference vector 
    """
    P = (16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25)
    return P


# In[20]:


def permutation(input_block):
    
    """
    Function that returns the permutation of the 32-bit input block 
    """
    # get permutation box
    P_box = get_P_box()
    
    # make a BitArray with length equal to the input_block
    output_block = BitArray(len(input_block))
    
    # perform permutation based on the P_box
    for index in range(len(input_block)):
        output_block[index] = input_block[P_box[index] -1 ]
    
    return output_block


# In[2]:


def round_function(input_block, round_key):
    
    """
    Function that implements the round functiuon and returns a corresponding output block after undergoing
    the following operations:
    
    Inputs: 32_bits input block, 48-bits round key 
    
    1. Expansion function on the input block to make it 48-bits
    2. XOR expanded input block with round key 
    3. Apply sbox transformation on the result of (2.)
    4. Apply permutation(Straight P )
      
    Outputs: result of step 4. 
        
    """
    # peform expansion
    output_block = expansion_function(input_block)
    
    # perform XOR with the round_key
    output_block = output_block ^ round_key
    
    # apply sbox calculation
    output_block = s_box_calculation(output_block)
    
    # apply permutation
    output_block = permutation(output_block)
    
    return output_block
    


# ## DES Key Generation Module 
# 
# #### Steps 
# 
# * 1. Parity drop - permutation choice 1 (PC-1)
# * 2. Circular Left shift function
# * 3. Compression P-box function

# In[4]:


def permutation_choice_1(initial_key):
    
    """
    Function that returns only 56 bits of the 64 bits input using a permutation table as reference  
    """
    # get PC1 table
    PC1 = (57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,
           43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,
           7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,
           28,20,12,4)
    
    # make an BitArray with size of PC1 (e.g., 56 bits)
    output_block = BitArray(len(PC1))
    
    # perform permutation choice 1
    for index in range(len(PC1)):
        output_block[index] = initial_key[PC1[index]-1]
    
    
    return output_block


# In[28]:


def get_key_rotation(round_number):
    
    """
    Function that returns the number of rotations based on the round number 
    """
    # define rotation table as a dictionary
    rotation_table = {1: 1,
                       2: 1,
                       3: 2,
                       4: 2,
                       5: 2,
                       6: 2,
                       7: 2,
                       8: 2,
                       9: 1,
                       10: 2,
                       11: 2,
                       12: 2,
                       13: 2,
                       14: 2,
                       15: 2,
                       16: 1
                      }
    
    return rotation_table[round_number]    


# **Exercise:** Implement `circular_shift()` that performs left rotation shift based on the number of rotations.

# In[30]:


def circular_left(input_block, rotation):
    """
    Function that performs circular shift and returns the output based on the number of rotations 
    """
    shifted_bits = input_block[rotation:len(input_block)] + input_block[0:rotation]
    return shifted_bits 


# **Exercise:** Implement `compression_pbox()` that performs *permutation_choice_2*. 

# In[5]:


def compression_pbox(input_block):
    
    """
    Function that performs permutation choice 2 using a compression table to compress 56 bits and retruns 48 bits
    """
    # get the PC2 vector (compression table)
    PC2 = (14,17,11,24,1,5,3,28,15,
           6,21,10,23,19,12,4,26,8,
           16,7,27,20,13,2,41,52,31,
           37,47,55,30,40,51,45,33,
           48,44,49,39,56,34,53,46,
           42,50,36,29,32)
    
    # make an BitArray with the size of PC2
    output_block = BitArray(len(PC2))
    
    # perform compression_P_box
    for index in range(len(PC2)):
        output_block[index] = input_block[PC2[index]-1]
        
    return output_block


# In[36]:


def key_generation(initial_key):
    
    """
    Function that returns a unique key depending on the round number and initial key
    
    """
    # make an empty dictionary to store each generate round keys
    round_key = {}
    
    # perform parity drop in initial_key
    output_block = permutation_choice_1(initial_key)
    
    # split output_block into left and right side
    split_index = int(len(output_block)/2)
    L0 = output_block[:split_index]
    R0 = output_block[split_index:]
    
    # getnerate keys for each round
    for round_number in range(1,17):
        # get the rotation based on the current round number
        rotation = get_key_rotation(round_number)
        
        # perfrom left shift on the left and right sides
        new_L = circular_left(L0,rotation)
        new_R = circular_left(R0,rotation)
        
        # apply the compression box on the shifted left and right
        round_key[round_number] =  compression_pbox(new_L + new_R)
        
        # update the L0 and R0 for the next round
        L0 = new_L
        R0 = new_R
    
    return round_key
    

    


# ## Round Function Algorithm 

# In[38]:


def feistel_round(input_block, round_key): 
    """
    
    Function that implements the procedure for each DES round in Feistel Algorithm using the pre-defined round_function() 
    """
    # get the left and right side of the input block
    split_index = int(len(input_block)/2)
    L_in = input_block[:split_index]
    R_in = input_block[split_index:]
    
    # assign right input side to the left output
    L_out = R_in
    
    # apply round function on the right input
    R_scrambled = round_function(R_in,round_key)
    
    # XOR R_scrambled with Left input and assign it to Right output
    R_out = R_scrambled ^ L_in
    
    # concatenate left and right output as an output_block
    output_block = L_out + R_out 
    
    return output_block


# ## DES Implementation

# In[7]:


def des_cipher(input_block, initial_key, mode='E'):
    
    """
    Function that implements DES encryption/decryption dependent on the input mode
    - Key Schedule algorithm
    - Initialm permutation
    - Round function
    - Final permutation
    """
    
    # generate key rounds based on the initial key
    round_keys = key_generation(initial_key)   
    # perform initial permutation
    output_block = init_permute(input_block)
    
    # perform Feistel round operations
    for i in range(0,16):
        
        # reverse the application of round keys is the mode is not E (encryption)
        
        if (mode == 'E'):
            round_num = i+1
            
        else:
            round_num = 16 - i
        
        # apply round operation
        output_block = feistel_round(output_block,round_keys[round_num])
        
    
    # perform 32-bit swap
    split_index = int(len(output_block)/2)
    output_block = output_block[split_index:] + output_block[:split_index]
    
    # perform final permutation
    output_block = final_permutation(output_block)
    
    
    
    return output_block
        
        


# In[ ]:





# In[ ]:




