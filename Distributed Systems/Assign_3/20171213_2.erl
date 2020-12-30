-module('20171213_2').

-export([main/1, readlines/1, msort/2, splitlist/2, mergefun/2, mergefun/3, append/2, print/2]).

%function to parse values
readlines(FileName) ->
    	{ok, Data} = file:read_file(FileName),
    	StringData = string:lexemes(string:tokens(erlang:binary_to_list(Data), "\n") , " "),
    	[list_to_integer(Item) || Item <- StringData ].

%main function
main(Args) ->
	[Input, Output] = Args,
	Arr = readlines(Input),
	Pid = spawn(?MODULE, msort, [self(), Arr]),	
	receive
    		{ Pid, SArr } -> 
			    SArr
    end,

% printing to file
       {ok, _} = file:open(Output, [write]),
       print(SArr, Output).

%function to print element by element into file
print([],File) ->
       {ok, FFile} = file:open(File, [append]),
       io:fwrite(FFile," \n", []);

print([H|T],File) ->
      {ok, FFile} = file:open(File, [append]), 
      io:fwrite(FFile, "~p ", [H]),
      print(T,File).

%main merge sort function
msort(Pid, Arr) ->
	if 
	        length(Arr) == 1 ->	
			Pid ! { self(), Arr };
		
		true ->	  	
		   {LeftArr, RightArr} = splitlist(Arr, length(Arr) div 2),
		   PidL = spawn(?MODULE, msort, [self(), LeftArr]),	
		   PidR = spawn(?MODULE, msort, [self(), RightArr]),
	   	   receive
			{ PidL, LSArr } ->
				LSArr
		   end,
   		   receive
			{ PidR, RSArr } ->
				RSArr
		   end,
   		   Pid ! { self(), mergefun(LSArr, RSArr) }
	end.

%to split list recursively
splitlist([H|L], S) ->
	if 
		S == 0 ->
		   {[], [H|L]};
	     	true ->	
		   { LArr, RArr } = splitlist(L,S-1),
	       	   { [H|LArr], RArr}
	end.

%append function
append([H|T], AppArr) ->
    [H|append(T, AppArr)];

append([], AppArr) ->
    AppArr.


% mergefunction implemented
mergefun(Arr1, Arr2) ->
	mergefun(Arr1, Arr2, []).

mergefun([], [], SArr) -> 
	SArr;

mergefun([], Arr2, SArr) ->
	append(SArr,Arr2);

mergefun(Arr1, [], SArr) ->
	append(SArr,Arr1);

mergefun([H1|Arr1], [H2|Arr2], SArr ) ->

	if 
		H1 > H2 ->
			mergefun([H1|Arr1], Arr2, append(SArr,[H2]));
		
		true ->
			mergefun(Arr1, [H2|Arr2], append(SArr,[H1]))
	end.
