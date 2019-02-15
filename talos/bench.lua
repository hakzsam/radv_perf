RunAsync(function()
  -- wait until start screen is shown
  Wait(CustomEvent("StartScreen_Shown"));
  -- handle initial interactions
  gamHandleInitialInteractions();
  
  -- use medium speed by default
  prj_psGameOptionPlayerSpeed = 1;
  -- make sure developer cheats are enabled
  cht_bEnableCheats = 2;
  -- enable the bot
  cht_bAutoTestBot = 1;
  -- optional: make bot skip terminals and QR codes
  bot_bSkipTerminalsAndMessages = 1;
  -- start a new game
  local episode = "Content/Talos/Levels/Demo.nfo"
  bmk_bAutoQuit = 1;
  bmkStartBenchmarking(3, 30);
  prjStartNewTalosGame(episode);
  Wait(Delay(45))
  bmkResults();
  Quit();
  
  -- wait until game ends
  BreakableRunHandled(
    WaitForever,
    -- if fame ended
    On(CustomEvent("GameEnded")),
    function()
      print("Finished auto test bot run");
      BreakRunHandled();
    end,
    -- if test bot failed
    On(CustomEvent("AutoTestBot_Failed")),
    function()
      BreakRunHandled();
    end
  )
  -- quit the game after finished running the auto test bot
  quit();
end);
