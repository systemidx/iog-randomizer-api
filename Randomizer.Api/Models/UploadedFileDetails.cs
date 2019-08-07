namespace Randomizer.Api.Models
{
    public struct UploadedFileDetails
    {
        public string Directory { get; set; }
        public string FileName { get; set; }
        public string Extension { get; set; }
        public string FullPath { get; set; }
    }
}