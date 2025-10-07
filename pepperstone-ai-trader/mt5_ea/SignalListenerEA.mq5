//+------------------------------------------------------------------+
//| SignalListenerEA.mq5                                             |
//| Lê sinais de CSV: SYMBOL,SIDE,LOT,CONF,TS                        |
//+------------------------------------------------------------------+
#property copyright ""
#property version "1.00"
#property strict

input string SignalFile = "C:\\signal_folder\\signals.csv"; // Caminho completo do CSV
input int Slippage = 20; // Slippage máximo

// Função principal chamada a cada tick
void OnTick()
{
    static datetime lastCheck = 0;
    if(TimeCurrent() - lastCheck < 1) return; // não verificar a cada tick
    lastCheck = TimeCurrent();
    ProcessSignals();
}

// Função para processar sinais CSV
void ProcessSignals()
{
    int fh = FileOpen(SignalFile, FILE_READ|FILE_CSV|FILE_ANSI);
    if(fh == INVALID_HANDLE)
    {
        Print("Erro ao abrir arquivo: ", SignalFile);
        return;
    }

    while(!FileIsEnding(fh))
    {
        string symbol, side;
        double lot, conf;
        long ts;

        // Ler linha do CSV
        if(FileReadString(fh) != "") // ignora linhas vazias
        {
            symbol = FileReadString(fh);
            side   = FileReadString(fh);
            lot    = FileReadNumber(fh);
            conf   = FileReadNumber(fh);
            ts     = (long)FileReadNumber(fh);

            if(SymbolSelect(symbol, true))
            {
                ExecuteTrade(symbol, side, lot, Slippage);
            }
        }
    }

    FileClose(fh);
}

// Função para enviar ordens
void ExecuteTrade(string symbol, string side, double lot, int slippage)
{
    double price = 0;
    ENUM_ORDER_TYPE type;

    if(side == "BUY")
    {
        type = ORDER_TYPE_BUY;
        price = SymbolInfoDouble(symbol, SYMBOL_ASK);
    }
    else if(side == "SELL")
    {
        type = ORDER_TYPE_SELL;
        price = SymbolInfoDouble(symbol, SYMBOL_BID);
    }
    else
    {
        Print("Sinal inválido: ", side);
        return;
    }

    MqlTradeRequest request;
    MqlTradeResult result;
    ZeroMemory(request);
    ZeroMemory(result);

    request.action   = TRADE_ACTION_DEAL;
    request.symbol   = symbol;
    request.volume   = lot;
    request.type     = type;
    request.price    = price;
    request.deviation= slippage;
    request.magic    = 123456;
    request.type_filling = ORDER_FILLING_FOK;

    if(!OrderSend(request, result))
    {
        Print("Erro ao enviar ordem: ", result.retcode);
    }
    else
    {
        Print("Ordem enviada: ", side, " ", symbol, " lote: ", lot);
    }
}
