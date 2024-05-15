# Sequence-Alignment
This is a famous problem where we have two RNA sequences (strings consisting of 'A', 'T', 'C', 'G') of different/same length and we want to align the two sequnece to maiximize their similarity. The alignment cost tells us how similar the two sequences are. This is a famous problem in computational biology. We are given two sequences, mismatch cost (if 'A' is not aligned with 'A', there is a penalty), and gap cost (a letter may be aligned with a gap '_', which also incurs a penalty).

# INPUT
The input file is a blueprint to generate two random sequences. The code takes this input file and does some processing to get two sequences. Consider the following input as an example:

ACTG

3

6

1 

TACG 

1

2

9

Base string: ACTG

Insertion after index 3: ACTGACTG

Insertion after index 6: ACTGACTACTGACTGG

Insertion after index 1: ACACTGACTACTGACTGGTGACTACTGACTGG

Similarly,

TACG

TATACGCG

TATTATACGCGACGCG 

TATTATACGCTATTATACGCGACGCGGACGCG

Thus, using the inputs above, the generated strings are:

ACACTGACTACTGACTGGTGACTACTGACTGG 

and 

TATTATACGCTATTATACGCGACGCGGACGCG 

which now need to be aligned.

# OUTPUT
Output file consists of following lines:
1. Cost of the alignment (Integer)
2. First string alignment ( Consists of A, C, T, G, _ (gap) characters)
3. Second string alignment ( Consists of A, C, T, G, _ (gap) characters )
4. Time in Milliseconds (Float)
5. Memory in Kilobytes (Float)

# ALGORITHM
This problem can be solved using a dynamic programming (DP) approach. However, the pure DP approach is not memory efficient, i.e., it needs to create a full DP table of size len(string1)*len(string2). This may be impractical due to the fact that a real RNA sequence can be very long and it would be impossible to store this huge DP table into the memory.
That is why we use DP along with Divide and Conquer (DC) approach. DP, combined with DC allows us to use linear memory.
Pure DP approach time complexity: O(MN)
Efficient DP (DP+DC) approach time complexity: O(MN)
Pure DP approach space complexity: O(MN)
Efficient DP (DP+DC) approach space complexity: O(M+N)
where M and N are the lengths of the strings

For detailed explanation of how this efficient algorithm works, please refer to: Algorithm Design book by Jon Kleinberg and Éva Tardos.

# Running the code

Run the code by executing the following line in the terminal:

```sh
python3 eff_3_class.py <input file name> <output file name>
