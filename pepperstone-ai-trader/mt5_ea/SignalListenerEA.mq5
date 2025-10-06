//+------------------------------------------------------------------+
//| SignalListenerEA.mq5 |
//| Le sinais em CSV: SYMBOL,SIDE,LOT,CONF,TS |
//+------------------------------------------------------------------+
#property copyright ""
#property version "1.00"
#property strict


input string SignalFolder = "C:\\signal_folder\\";
input double MaxRiskPercent = 1.0; // ex: 1% por trade (geralmente calculado fora)
input int Slippage = 20;


void OnTick()
{
static datetime lastCheck = 0;
if(TimeCurrent() - lastCheck < 1) return; // não verificar a cada tick
lastCheck = TimeCurrent();
ProcessSignals();
}


void ProcessSignals()
{
string pattern = SignalFolder + "signal_*.csv";
int files = FileFindFirst(pattern);
if(files==INVALID_HANDLE) return;
string filename;
while(FileFindNext(files, filename))
{
string full = SignalFolder + filename;
int fh = FileOpen(full, FILE_READ|FILE_ANSI);
if(fh!=INVALID_HANDLE)
{
string line = FileReadString(fh, FileSize(full));
FileClose(fh);
// parse CSV
string parts[];
int n = StringSplit(line, ',', parts);
if(n>=5)
{
string symbol = parts[0];
string side = parts[1];
double lot = StrToDouble(parts[2]);
double conf = StrToDouble(parts[3]);
// safety checks
if(SymbolInfoDouble(symbol, SYMBOL_TRADE_CO