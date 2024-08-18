// Copyright 2024 John Hanley. MIT licensed.
// from https://stackoverflow.com/questions/76857440/how-to-sort-integers-in-a-sequence-in-dafny

method sort(a: seq<int>) returns (r: seq<int>)
  ensures |a| == |r|
  ensures multiset(a) == multiset(r)
  ensures forall i,j :: 0 <= i <= j < |r| ==> r[i] <= r[j]
{
  if |a| <= 1 {
    return a;
  }else{
   var head := a[0];
   var tail := a[1..];
   assert a == a[0] + a[1..]; //Frequently you must include this for extensionality.
   //Do some sorting here.
  }
}

method Main() {
  print(2 + 3);
  print("\n");
}
