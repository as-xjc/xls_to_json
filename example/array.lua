--[[
xls path: example/test.xls
]]--

local hander = {}

local __data__ = {
  {
      ["id"] = 1,
      ["game_list"] = {
          "wow",
          "lol",
          1,
          {
              ["1"] = {
                  1,
                  2,
                  3,
                  1000,
                  5,
              },
          },
      },
      ["is_man"] = false,
      ["name"] = "hey",
      ["property"] = {
          ["learn"] = "pc",
          ["game"] = 10,
      },
  },
  {
      ["id"] = 2,
      ["game_list"] = {
          12313,
          "lol",
          23.1,
      },
      ["is_man"] = true,
      ["name"] = "hahaha",
      ["property"] = {
          ["buy"] = "pc",
          ["你好"] = 10,
      },
  },
}

function hander.getData()
	return __data__
end

-- ========== custom your code area start ==========
-- ========== custom your code area end ==========


return hander