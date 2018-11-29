//read file
val data = scala.io.Source.fromFile("dow_jones_index.data").getLines

//convert iterator to Array
val data_arr = data.toArray.drop(1)

//create StockPrice case class
case class StockPrice(quarter: String,
  stock: String,
  date: String ,
  open: Float,
  high : Float,
  low: Float,
  close: Float,
  volume: Int,
  percent_change_price: String,
  percent_change_volume_over_last_wk: String,
  previous_weeks_volume: String,
  next_weeks_open: String,
  next_weeks_close: String,
  percent_change_next_weeks_price: String,
  days_to_next_dividend: String,
  percent_return_next_dividend: String)

//split string by comma then change array of strings to StockPrice class
def convert_data(x: String):StockPrice={
  var arr = x.split(",")
  var y = StockPrice(arr(0),arr(1), arr(2), arr(3).substring(1).toFloat, arr(4).substring(1).toFloat,arr(5).substring(1).toFloat, arr(6).substring(1).toFloat, arr(7).toInt,arr(8), arr(9), arr(10), arr(11), arr(12),arr(13),arr(14), arr(15))
  return y}

val data_cc = data_arr.map(convert_data(_))

//use match-case to fin min, max, avrage by condition
def get_match(x: StockPrice,stock: String):Int = {
  x.stock match {case y if y == stock => return x.volume
  case _ => return 0}}

val PFE = data_cc.map(get_match(_,"PFE"))
val av_PFE = PFE.foldLeft(0)(_+_) / PFE.size
val min_PFE = PFE.min
val max_PFE = PFE.max

//use groupBy to find min, max by stock name
val group_max = data_cc.groupBy(d =>(d.stock)).map{case(k,v) => (k,v.map(_.open).max)}
val group_min = data_cc.groupBy(d =>(d.stock)).map{case(k,v) => (k,v.map(_.open).min)}

// find min, max gap
val gap = data_cc.groupBy(d =>(d.stock)).map{case(k,v) => (k,v.map(_.open).max-v.map(_.open).min)}
val max_gap = gap.max._1 //max_gap: String = XOM
val min_gap = gap.min._1 //min_gap: String = AA

//the date that the gap between open and close price is maximum
val open_close = data_cc.map{p =>(p.date, p.close-p.open match{case x if x>0 => x
  case x if x<0 => -x
  case _ =>0})}

val max_change = open_close.max._1 //max_change: String = 6/3/2011
