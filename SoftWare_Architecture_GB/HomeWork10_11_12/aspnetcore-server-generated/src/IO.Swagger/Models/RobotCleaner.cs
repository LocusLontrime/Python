/*
 * Сервис роботов-пылесосов
 *
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 0.0.1
 * 
 * Generated by: https://github.com/swagger-api/swagger-codegen.git
 */
using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;
using Newtonsoft.Json;

namespace IO.Swagger.Models
{ 
    /// <summary>
    /// 
    /// </summary>
    [DataContract]
    public partial class RobotCleaner : IEquatable<RobotCleaner>
    { 
        /// <summary>
        /// Gets or Sets Resources
        /// </summary>
        [Required]

        [DataMember(Name="resources")]
        public int? Resources { get; set; }

        /// <summary>
        /// Gets or Sets FabrickNumber
        /// </summary>
        [Required]

        [DataMember(Name="fabrick_number")]
        public int? FabrickNumber { get; set; }

        /// <summary>
        /// Gets or Sets IpAdress
        /// </summary>
        [Required]

        [DataMember(Name="ip_adress")]
        public string IpAdress { get; set; }

        /// <summary>
        /// Gets or Sets IdGroup
        /// </summary>
        [Required]

        [DataMember(Name="id_group")]
        public int? IdGroup { get; set; }

        /// <summary>
        /// Gets or Sets Status
        /// </summary>
        [Required]

        [DataMember(Name="status")]
        public string Status { get; set; }

        /// <summary>
        /// Returns the string presentation of the object
        /// </summary>
        /// <returns>String presentation of the object</returns>
        public override string ToString()
        {
            var sb = new StringBuilder();
            sb.Append("class RobotCleaner {\n");
            sb.Append("  Resources: ").Append(Resources).Append("\n");
            sb.Append("  FabrickNumber: ").Append(FabrickNumber).Append("\n");
            sb.Append("  IpAdress: ").Append(IpAdress).Append("\n");
            sb.Append("  IdGroup: ").Append(IdGroup).Append("\n");
            sb.Append("  Status: ").Append(Status).Append("\n");
            sb.Append("}\n");
            return sb.ToString();
        }

        /// <summary>
        /// Returns the JSON string presentation of the object
        /// </summary>
        /// <returns>JSON string presentation of the object</returns>
        public string ToJson()
        {
            return JsonConvert.SerializeObject(this, Formatting.Indented);
        }

        /// <summary>
        /// Returns true if objects are equal
        /// </summary>
        /// <param name="obj">Object to be compared</param>
        /// <returns>Boolean</returns>
        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            return obj.GetType() == GetType() && Equals((RobotCleaner)obj);
        }

        /// <summary>
        /// Returns true if RobotCleaner instances are equal
        /// </summary>
        /// <param name="other">Instance of RobotCleaner to be compared</param>
        /// <returns>Boolean</returns>
        public bool Equals(RobotCleaner other)
        {
            if (ReferenceEquals(null, other)) return false;
            if (ReferenceEquals(this, other)) return true;

            return 
                (
                    Resources == other.Resources ||
                    Resources != null &&
                    Resources.Equals(other.Resources)
                ) && 
                (
                    FabrickNumber == other.FabrickNumber ||
                    FabrickNumber != null &&
                    FabrickNumber.Equals(other.FabrickNumber)
                ) && 
                (
                    IpAdress == other.IpAdress ||
                    IpAdress != null &&
                    IpAdress.Equals(other.IpAdress)
                ) && 
                (
                    IdGroup == other.IdGroup ||
                    IdGroup != null &&
                    IdGroup.Equals(other.IdGroup)
                ) && 
                (
                    Status == other.Status ||
                    Status != null &&
                    Status.Equals(other.Status)
                );
        }

        /// <summary>
        /// Gets the hash code
        /// </summary>
        /// <returns>Hash code</returns>
        public override int GetHashCode()
        {
            unchecked // Overflow is fine, just wrap
            {
                var hashCode = 41;
                // Suitable nullity checks etc, of course :)
                    if (Resources != null)
                    hashCode = hashCode * 59 + Resources.GetHashCode();
                    if (FabrickNumber != null)
                    hashCode = hashCode * 59 + FabrickNumber.GetHashCode();
                    if (IpAdress != null)
                    hashCode = hashCode * 59 + IpAdress.GetHashCode();
                    if (IdGroup != null)
                    hashCode = hashCode * 59 + IdGroup.GetHashCode();
                    if (Status != null)
                    hashCode = hashCode * 59 + Status.GetHashCode();
                return hashCode;
            }
        }

        #region Operators
        #pragma warning disable 1591

        public static bool operator ==(RobotCleaner left, RobotCleaner right)
        {
            return Equals(left, right);
        }

        public static bool operator !=(RobotCleaner left, RobotCleaner right)
        {
            return !Equals(left, right);
        }

        #pragma warning restore 1591
        #endregion Operators
    }
}