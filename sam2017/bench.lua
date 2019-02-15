RunAsync(function()
  prj_bStartupAutoDetection = 0;

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
  gam_strLevel = "0_02_SandCanyon"
  bmk_bAutoQuit = 1;
  bmkStartBenchmarking(3, 30);
  gamStart();
  Wait(Delay(36))
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
