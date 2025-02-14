// leaving naive version in place to experience the shame
class Stones(input:String):
    var numbers : List[BigInt] = input.split(' ').map(BigInt(_)).toList
    var cache = scala.collection.mutable.Map[BigInt, List[BigInt]]()

    def replaced(x:BigInt):List[BigInt] =
        // adding cache lets Part 2 get to 40 cycles
        // instead of 39, before just giving up
        if cache.contains(x) then
            return cache(x)

        val s = x.toString
        val result =
            if x == 0 then
                List(BigInt(1))
            else if s.size % 2 == 0 then
                List(
                    BigInt(x.toString.take(s.size / 2)),
                    BigInt(x.toString.drop(s.size / 2)))
            else
                List(x * 2024)
        cache(x) = result
        result


    def blink =
        numbers = numbers.map(replaced(_)).flatten()

    def doBlinks(n: Int) : Stones =
        for i <- 1 to n do
            blink
            println(s"blink[$i] at [${java.time.LocalTime.now}] size [${numbers.size}]")
        this

//////////////////
// Now the real solution
class Stones2(input:String):
    var numbers = scala.collection.mutable.Map[BigInt, BigInt]()
    for number <- input.split(" ") do
        numbers(BigInt(number)) = 1

    def replaced(x:BigInt):List[BigInt] =
        val s = x.toString
        if x == 0 then
            List(BigInt(1))
        else if s.size % 2 == 0 then
            List(
                BigInt(x.toString.take(s.size / 2)),
                BigInt(x.toString.drop(s.size / 2)))
        else
            List(x * 2024)

    def blink =
        var newNumbers = scala.collection.mutable.Map[BigInt, BigInt]()
        for (number, count) <- numbers do
            for replacement <- replaced(number) do
                if newNumbers.contains(replacement) then
                    newNumbers(replacement) += count
                else
                    newNumbers(replacement) = count
        numbers = newNumbers

    def doBlinks(n: Int) : Stones2 =
        for i <- 1 to n do
            blink
            println(s"blink[$i] at [${java.time.LocalTime.now}] size [${totalCount}]")
            println(numbers)
        this

    def totalCount = numbers.values.sum

class Day11(filename:String):
    val lines = io.Source
        .fromFile("src/day-11/" + filename)
        .getLines.toList

    def part1 = Stones2(lines(0)).doBlinks(25).totalCount
    def part2 = Stones2(lines(0)).doBlinks(75).totalCount

Day11("input.txt").part1   // 197157
Day11("input.txt").part2   // 234430066982597
