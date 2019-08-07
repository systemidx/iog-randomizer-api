namespace Randomizer.Api.Models
{
    public class SeedParameters
    {
        public string Difficulty { get; set; } = "Normal";
        public string Goal { get; set; } = "Dark Gaia";
        public string Variations { get; set; } = "None";
        public bool Firebird { get; set;  } = false;
        public string Mode { get; set; } = "Completable";
        public string Statues { get; set; } = "4";
    }
}