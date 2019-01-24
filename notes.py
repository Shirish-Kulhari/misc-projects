"""
About Numpy strides: Say that you have a Numpy array X = [[1,2,3],[4,5,6]] => 2 rows, 3 columns. Dimension 0 (rows) has 2 items and dimension 1 (columns) has 3. The array elements are stored in continuous locations: (1)(2)(3)(4)(5)(6) => this is the DEFAULT way. Another way to store them in contiguous locations is: (1)(4)(2)(5)(3)(6).

An array has a "stride size" for each dimension : the first element has indices 0 corresponding to all the dimensions, i.e., X[0][0]. Starting from the first element, how many elements should we traverse to increment the index for that particular dimension (while keeping indices for other dimensions the same)?

Stride size for dimension 0: how many elements should we traverse to increment the index for 0-th dimension (or to get to the next row)? Obviously in this case, 3 elements OR 6 bytes (int16 size is 2 bytes). So stride size is 6.

Stride size for dimension 1: we just have to traverse 1 element (2 bytes) to get to an element ((2)) with a greater column index (1). So the strides tuple will be (6,2).

Another example: [[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]]  OR
[[[ 1  2  3]        ==> Let's call this "slice 0"
  [ 4  5  6]]

 [[ 7  8  9]
  [10 11 12]]]      ==> "Slice 1"

So [4,5,6] is slice 0, row 1, and [7,10] is slice 1, column 0.

Now dimension 0 is NOT the row, but the slice. The way the elements are stored is: (1)(2)(3)...(10)(11)(12). From the first element (1), to increment dimension 0 index (i.e. to get to the next slice), we have to traverse 6 elements or 12 bytes. Similarly, stride size for dimensions 1 and 2 are 6 and 2 respectively.
"""
