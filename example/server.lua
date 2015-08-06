--[[
xls path: example/test.xls
]]--

return 
{
  [1] = {
      ["is_man"] = false,
      ["name"] = "hey",
      ["id"] = 1,
      ["game_list"] = {
          [1] = "wow",
          [2] = "lol",
          [3] = 1,
          [4] = {
              ["1"] = {
                  [1] = 1,
                  [2] = 2,
                  [3] = 3,
                  [4] = 1000,
                  [5] = 5,
              },
          },
      },
  },
  [2] = {
      ["is_man"] = true,
      ["name"] = "hahaha",
      ["id"] = 2,
      ["game_list"] = {
          [1] = 12313,
          [2] = "lol",
          [3] = 231,
      },
  },
}
