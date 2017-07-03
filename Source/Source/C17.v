module C17( 1, 2, 22, 23, 3, 6, 7);

	output  22, 23;
	input  1, 2, 3, 6, 7;
	wire  10, 11, 16, 19;


	nand instance_0(10, 3, 1 );
	nand instance_1(11, 6, 3 );
	nand instance_2(16, 11, 2 );
	nand instance_3(19, 7, 11 );
	nand instance_4(22, 16, 10 );
	nand instance_5(23, 19, 16 );


endmodule
