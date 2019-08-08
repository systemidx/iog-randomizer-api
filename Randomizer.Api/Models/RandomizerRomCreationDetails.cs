namespace Randomizer.Api.Models
{
    public struct RandomizerRomCreationDetails
    {
        public bool Success {get; set;}
        public string RomPath { get; set; }
        public string Error {get; set;}
    }
}