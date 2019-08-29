using System;
using System.Collections.Generic;
using System.Linq;

namespace Randomizer.Api.Models
{
    public class SeedParameters
    {        
        public long Seed { get; set; } = DateTime.UtcNow.Ticks;
        public string Difficulty { get; set; } = "Normal";
        public string Goal { get; set; } = "Dark Gaia";
        public string Enemizer { get; set; } = "None";
        public string StartPosition { get; set; } = "South Cape";
        public bool Firebird { get; set;  } = false;
        public string Logic { get; set; } = "Completable";
        public string Statues { get; set; } = "4";
        public bool AllowGlitches { get; set; } = false;
        public bool OneHitKnockOut { get; set; } = false;
        public bool RedJewelMadness { get; set; } = false;
        public bool BossShuffle { get; set; } = false;
        public string EntranceShuffle { get; set; } = "None";
        public bool DungeonShuffle { get; set; } = false;
        public bool OverworldShuffle { get; set; } = false;
        public string Variations
        {
            get
            {
                var variations = new List<string>();

                if (AllowGlitches)
                    variations.Add("AllowGlitches");
                
                if (OneHitKnockOut)
                    variations.Add("OHKO");
                else if (RedJewelMadness)
                    variations.Add("Red Jewel Madness");

                if (DungeonShuffle)
                    variations.Add("Dungeon Shuffle");
                
                if (OverworldShuffle)
                    variations.Add("Overworld Shuffle");

                if (BossShuffle)
                    variations.Add("Boss Shuffle");

                if (variations.Any())
                    return string.Join(',', variations);

                return "None";
            }
        }
    }
}
